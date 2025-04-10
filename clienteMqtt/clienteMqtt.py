import asyncio, ssl, os, logging
import aiomqtt
import certifi

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s:%(message)s',
    level=logging.INFO,
    datefmt='%d/%m/%Y %H:%M:%S'
)

# Función para manejar mensajes de un solo consumidor
async def recibir_mensajes(client, topicos):
    logger = logging.getLogger("Receptor")
    for topico in topicos:
        await client.subscribe(topico)

    async for message in client.messages:
        topico = str(message.topic)
        if topico in topicos:
            logger.info(f"[{topico}] {message.payload.decode('utf-8')}")

async def cliente_mqtt():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_verify_locations(cafile=certifi.where())

    async with aiomqtt.Client(
        hostname=os.environ['SERVIDOR'],
        port=8883,
        tls_context=tls_context
    ) as client:
        # Lista de tópicos a suscribirse
        topicos = [os.environ['TOPICO1'], os.environ['TOPICO2']]
        await recibir_mensajes(client, topicos)

if __name__ == "__main__":
    try:
        asyncio.run(cliente_mqtt())
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
