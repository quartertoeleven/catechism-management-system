from dependency_injector import containers, providers

from services.health_service import HealthService


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    health_service = providers.Singleton(
        HealthService,
        version=config.version,
    )

    wiring_config = containers.WiringConfiguration(
        modules=["controllers.health_controller"],
    )
