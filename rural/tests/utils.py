from validate_docbr import CPF

from rural.models import Culture, Producer


class SetupTestMixin:

    def get_producer_obj(
        self,
        cpf_cnpj='',
        nome_produtor="Produtor Teste",
        nome_fazenda="Fazenda Teste",
        estado="SP",
        cidade="Sao Paulo",
        area_fazenda_ha=0,
        area_agricultavel_ha=0,
        area_vegetacao_ha=0
    ):
        cpf = CPF()
        producer = {
            "cpf_cnpj": cpf.generate() if not cpf_cnpj else cpf_cnpj,
            "nome_produtor": nome_produtor,
            "nome_fazenda": nome_fazenda,
            "estado": estado,
            "cidade": cidade,
            "area_fazenda_ha": area_fazenda_ha,
            "area_agricultavel_ha": area_agricultavel_ha,
            "area_vegetacao_ha": area_vegetacao_ha
        }
        return producer

    def make_producer(
        self,
        cpf_cnpj='',
        nome_produtor="Produtor Teste",
        nome_fazenda="Fazenda Teste",
        estado="SP",
        cidade="Sao Paulo",
        area_fazenda_ha=0,
        area_agricultavel_ha=0,
        area_vegetacao_ha=0
    ):
        producer_obj = self.get_producer_obj(
            cpf_cnpj=cpf_cnpj,
            nome_produtor=nome_produtor,
            nome_fazenda=nome_fazenda,
            estado=estado,
            cidade=cidade,
            area_fazenda_ha=area_fazenda_ha,
            area_agricultavel_ha=area_agricultavel_ha,
            area_vegetacao_ha=area_vegetacao_ha
        )
        producer = Producer.objects.create(**producer_obj)
        return producer
    
    def make_culture(self, nome="Cultura Teste"):
        culture = Culture.objects.create(
            nome=nome
        )
        return culture

    def make_producer_with_culture(self, qtd_culture=1):
        producer = self.make_producer()
        culture_list = [self.make_culture() for i in range(qtd_culture)]
        producer.cultura_vegetal.add(*culture_list)
        return producer
