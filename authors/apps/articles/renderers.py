from rest_framework.renderers import JSONRenderer
import json


class AuthorsJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_object_count = 'count'

    def render(self, data, media_type=None, renderer_context=None):
        if data.get('results', None) is not None:
            return json.dumps({
                self.pagination_object_label: data['results'],
                self.pagination_count_label: data['count']
            })

        # If the view throws an error (such as the user can't be authenticated
        # default json handler should handle

        elif data.get('errors', None) is not None:
            return super(AuthorsJSONRenderer, self).render(data)

        else:
            return json.dumps({
                self.object_label: data
            })


class ArticleJSONRenderer(AuthorsJSONRenderer):
    object_label = 'article'
    pagination_object_label = 'articles'
    pagination_count_label = 'articlesCount'







