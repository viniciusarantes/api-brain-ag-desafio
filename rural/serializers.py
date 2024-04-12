import re

from rest_framework import serializers, status

from rural.exceptions import CustomValidationException
from rural.models import Culture, Producer
from rural.validators import ProducerValidator

CULTURE_ADD_ACTION = 'add'
CULTURE_REMOVE_ACTION = 'remove'


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'nome', 'ultima_atualizacao']


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'
        depth = 1
    
    def create(self, validated_data):
        instance = Producer.objects.create(**validated_data)
        instance.cpf_cnpj = re.sub('[^0-9]', '', instance.cpf_cnpj)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.cpf_cnpj = re.sub('[^0-9]', '', instance.cpf_cnpj)
        instance.save()
        return instance
    
    def get_area_data(self, data):
        farm_ha = data.get('area_fazenda_ha', 0)
        agro_ha = data.get('area_agricultavel_ha', 0)
        veg_ha = data.get('area_vegetacao_ha', 0)

        obj_farm_ha = 0 if self.instance is None else self.instance.area_fazenda_ha
        obj_agro_ha = 0 if self.instance is None else self.instance.area_agricultavel_ha
        obj_veg_ha = 0 if self.instance is None else self.instance.area_vegetacao_ha
        return (
            farm_ha or obj_farm_ha, 
            agro_ha or obj_agro_ha, 
            veg_ha or obj_veg_ha
        )
    
    def get_cpf_cnpj(self, data):
        cpf_cnpj = data.get('cpf_cnpj', '')
        obj_cpf_cnpj = '' if self.instance is None else self.instance.cpf_cnpj
        return cpf_cnpj or obj_cpf_cnpj
    
    def validate(self, attrs):
        data = super().validate(attrs)
        cpf_cnpj = self.get_cpf_cnpj(data)
        doc_is_valid = ProducerValidator.validate_cpf_cnpj(cpf_cnpj)
        if not doc_is_valid:
            raise CustomValidationException(
                "CPF/CNPJ inválido. Digite um documento válido"
            )
        
        farm_ha, agro_ha, veg_ha = self.get_area_data(data)
        area_is_valid = ProducerValidator.validate_farm_area(
            farm_ha=farm_ha, agro_ha=agro_ha, veg_ha=veg_ha
        )
        if not area_is_valid:
            raise CustomValidationException(
                "Total da área agritultável e vegetação ultrapassa a área total da fazenda."
            )

        return data


class ProducerCulturesSerializer(serializers.Serializer):
    produtor_id = serializers.IntegerField()
    cultura_vegetal = serializers.ListField(
        child=serializers.IntegerField(min_value=0)
    )

    def get_object(self, obj_id, model_class):
        try:
            return model_class.objects.get(id=obj_id)
        except model_class.DoesNotExist:
            return None
    
    def to_representation(self, instance):
        cultura_vegetal = [
            dict(id=culture.id, nome=culture.nome) 
            for culture in instance.cultura_vegetal.all()
        ]
        data = {
            "id": instance.id,
            "nome_produtor": instance.nome_produtor,
            "cpf_cnpj": instance.cpf_cnpj,
            "cultura_vegetal": cultura_vegetal
        }
        return data
    
    def get_culture_list(self, cultures):
        obj_cultures, not_found_cultures = list(), list()
        for culture in cultures:
            obj_culture = self.get_object(culture, Culture)
            if obj_culture is None:
                not_found_cultures.append(culture)
            else:
                obj_cultures.append(obj_culture)
        return obj_cultures, not_found_cultures

    def create(self, validated_data):
        producer = self.get_object(validated_data.get('produtor_id'), Producer)
        culture_list, _ = self.get_culture_list(validated_data.get('cultura_vegetal'))
        if self.context.get('action') == CULTURE_ADD_ACTION:
            producer.cultura_vegetal.add(*culture_list)
        elif self.context.get('action') == CULTURE_REMOVE_ACTION:
            producer.cultura_vegetal.remove(*culture_list)
        producer.save()
        return producer
        
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        producer = self.get_object(validated_data.get('produtor_id'), Producer)
        if not producer:
            raise CustomValidationException(
                "Produtor id não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        _, not_found = self.get_culture_list(validated_data.get('cultura_vegetal'))
        if len(not_found) > 0:
            raise CustomValidationException(
                f"Culturas Vegetais não encontradas: {','.join(map(str, not_found))}",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return validated_data

