from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import frontend.chat.routing as chat_routing

application = ProtocolTypeRouter({
	# Empty for now (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			chat_routing.websocket_urlpatterns
		)
	),
})