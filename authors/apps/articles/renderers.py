from rest_framework.renderers import JSONRenderer
import json


class ArticleJSONRenderer(JSONRenderer):
    object_label = 'article'
    charset = 'utf-8'
    # pagination_object_label = 'articles'
    # pagination_count_label = 'articlesCount'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the articles in a structured manner for the end user.
        """
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'article': data
                })
            return json.dumps({
                'articles': data
            })
        return json.dumps({
            'article': 'No article found.'
        })
