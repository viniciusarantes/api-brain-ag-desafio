import validate_docbr as docbr


class ProducerValidator:

    @staticmethod
    def validate_cpf_cnpj(cpf_cnpj):
        docs = [(docbr.CPF, cpf_cnpj), (docbr.CNPJ, cpf_cnpj)]
        ret = docbr.validate_docs(docs)
        return True in ret
    
    @staticmethod
    def validate_farm_area(farm_ha, agro_ha, veg_ha):
        farm_ha = float(farm_ha)
        agro_ha = float(agro_ha)
        veg_ha = float(veg_ha)
        total_ha = agro_ha + veg_ha
        return total_ha <= farm_ha

    
