from rest_framework import serializers

from rural.models import Producer


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'
    
    def to_representation(self, instance):
        formatted_data = super().to_representation(instance)
        data = {
            "id": formatted_data.get("id"),
            "cpf_cnpj": formatted_data.get("cpf_cnpj"),
            "nome_produtor": formatted_data.get("name"),
            "nome_fazenda": formatted_data.get("farm_name"),
            "cidade": formatted_data.get("city"),
            "estado": formatted_data.get("state"),
            "area_fazenda_ha": formatted_data.get("farm_area_ha"),
            "area_agricultavel_ha": formatted_data.get("agro_area_ha"),
            "area_vegetacao_ha": formatted_data.get("veg_area_ha"),
            "cultura_vegetal": formatted_data.get("planting"),
            "criado_em": formatted_data.get("created"),
            "ultima_atualizacao": formatted_data.get("updated"),
        }
        return data