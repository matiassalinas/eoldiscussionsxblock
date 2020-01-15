"""
    This XBlock check for student participation on course discussions.
    Set a grade when the student participation (comments and thread created) is greater than min_participation attribute
"""

import pkg_resources

from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Integer, String, Scope
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

# Discussion signals
from django.dispatch import receiver
from django_comment_common  import signals
from xmodule.modulestore.django import SignalHandler

# Make '_' a no-op so we can scrape strings
_ = lambda text: text

# Django Logs
import logging
logger = logging.getLogger(__name__)

class EolDiscussionCheckXBlock(StudioEditableXBlockMixin, XBlock):

    display_name = String(
        display_name=_("Display Name"),
        help=_("Display name for this module"),
        default="Eol Discussions Check XBlock",
        scope=Scope.settings,
    )

    icon_class = String(
        default="problem",
        scope=Scope.settings,
    )

    discussion_id = String(
        display_name = _("ID Foro"),
        help = _("Indica el ID del foro/discusion. Recuerda que para el ID son 40 caracteres alfanumericos, ejemplo: fdbf5798b7d7672abac4c4f8af22404487c09c98"),
        default = "",
        scope = Scope.settings,
    )

    min_participation = Integer(
        display_name = _("Participacion Minima"),
        help = _("Indica la cantidad minima de participaciones del estudiante en el foro"),
        default = 1,
        values = { "min" : 1, "step" : 1 },
        scope = Scope.settings
    )

    weight = Integer(
        display_name='Peso',
        help='Puntaje maximo del problema',
        default=1,
        values={'min': 0},
        scope=Scope.settings,
    )

    editable_fields = ('discussion_id', 'min_participation', 'weight', )
    has_author_view = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/eoldiscussionscheck.html', context_html)
        frag = Fragment(template)

        frag.add_css(self.resource_string("static/css/eoldiscussionscheck.css"))
        frag.add_javascript(self.resource_string("static/js/src/eoldiscussionscheck.js"))
        frag.initialize_js('EolDiscussionCheckXBlock')
        return frag
    
    def author_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/author_view.html', context_html)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/eoldiscussionscheck.css"))
        return frag
    
    def get_context(self):
        return {
            'course_id': self.course_id,
            'discussion_id': self.discussion_id,
            'min_participation': self.min_participation
        }

    def render_template(self, template_path, context):
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))


    """
        Discussions signals
    """

    @receiver(signals.comment_created)
    @receiver(signals.thread_created)
    def discussion_signal_created(sender, user, post, **kwargs):
        """
            Trigger when student create a comment or a thread
        """
        logger.warning(user.id)
        logger.warning(post.course_id)
        logger.warning(post.commentable_id) # discussion id
        #logger.warning(dir(post))
        #logger.warning(post.to_dict())
        return

    @receiver(signals.comment_deleted)
    @receiver(signals.thread_deleted)
    def discussion_signal_deleted(sender, user, post, **kwargs):
        """
            Trigger when student delete a comment or a thread
        """
        logger.warning(user.id)
        logger.warning(post.course_id)
        logger.warning(post.commentable_id) # discussion id
        return

   
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("EolDiscussionCheckXBlock",
             """<eoldiscussionscheck/>
             """),
        ]
