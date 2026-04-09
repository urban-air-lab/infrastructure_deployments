FROM ubuntu:24.04 AS envsubst-builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext-base \
    && rm -rf /var/lib/apt/lists/*

FROM prom/alertmanager:v0.31.1
COPY --from=envsubst-builder /usr/bin/envsubst /usr/local/bin/envsubst
COPY --from=envsubst-builder /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=envsubst-builder /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2