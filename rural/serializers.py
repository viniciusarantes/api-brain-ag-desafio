import re

from rest_framework import serializers

from rural.exceptions import CustomValidationException
from rural.models import Planting, Producer
from rural.validators import ProducerValidator


class PlantingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planting
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

        