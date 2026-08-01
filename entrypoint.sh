#!/bin/bash
# entrypoint.sh for Zomboid Server Docker Container

# Check if admin password is provided
ADMIN_PASSWORD="${PZ_ADMIN_PASSWORD:-admin}"
SERVER_NAME="${PZ_SERVER_NAME:-servertest}"

echo "Starting Project Zomboid Server..."

# Run server with box64
/usr/local/bin/box64 /opt/zomboid-server/jre64/bin/java \
    -Djava.awt.headless=true \
    -Xms4g -Xmx16g \
    -XX:ActiveProcessorCount=4 \
    -Dzomboid.steam=1 \
    -Dzomboid.znetlog=1 \
    -Djava.library.path=linux64/:natives/ \
    -Djava.security.egd=file:/dev/urandom \
    -XX:+UseSerialGC \
    -XX:-UseCompressedOops \
    -XX:TieredStopAtLevel=1 \
    -cp "java/:java/projectzomboid.jar" \
    zombie.network.GameServer \
    -servername "$SERVER_NAME" \
    -adminpassword "$ADMIN_PASSWORD"
