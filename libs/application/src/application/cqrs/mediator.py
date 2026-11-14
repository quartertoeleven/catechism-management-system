"""CQRS request mediator wiring."""

from cqrs import RequestMap, RequestMediator, ScopeStrategy
from cqrs.bootstrap.requests import bootstrap
from cqrs.container.dishka import DishkaCQRSContainer
from dishka import AsyncContainer, Provider, Scope, provide

from application.cqrs.provider import REQUEST_HANDLERS


def bind_requests(mapper: RequestMap) -> None:
    """Bind every discovered request to its handler."""
    for registration in REQUEST_HANDLERS:
        mapper.bind(registration.request_type, registration.handler_type)


class RequestMediatorProvider(Provider):
    """Provide the CQRS request mediator."""

    def __init__(
        self,
        scope_strategy: ScopeStrategy = ScopeStrategy.SEND,
    ) -> None:
        self._scope_strategy = scope_strategy
        super().__init__()

    @provide(scope=Scope.APP)
    def request_mediator(self, container: AsyncContainer) -> RequestMediator:
        """Build the request mediator wired to this Dishka container."""
        return bootstrap(
            di_container=DishkaCQRSContainer(container),
            queries_mapper=bind_requests,
            scope_strategy=self._scope_strategy,
        )
