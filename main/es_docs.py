from  elasticsearch_dsl import Document, Long, Text, Keyword

class ESProduct(Document):
    name = Text(required = True)
    description = Text()
    price = Long(required = True)

    category = Keyword(required = True, index = 'false')
    tags = Text(multi = True)

    class Index:
        index = 'sample_index'
        name = 'sample_index'
        doc_type = 'products'