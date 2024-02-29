FROM docker.io/mambaorg/micromamba:1.5.6-bookworm-slim

RUN \
    --mount=type=cache,sharing=private,target=/home/mambauser/.mamba/pkgs,uid=57439,gid=57439 \
    --mount=type=cache,sharing=private,target=/opt/conda/pkgs,uid=57439,gid=57439 \
    micromamba -y -n base install -c conda-forge python=3.6 nibabel=4.0.2 numpy=1.19.5

ARG SRCDIR=/home/mambauser/src
RUN mkdir "${SRCDIR}"
WORKDIR ${SRCDIR}

COPY . .
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN pip install . && cd / && rm -rf ${SRCDIR}
WORKDIR /

ENV PATH=/opt/conda/bin:$PATH

CMD ["correct_MALP-EM_map.py"]

LABEL org.opencontainers.image.authors="Stefan Pszczolkowski Parraguez <stefan.pszczolkowskiparraguez@nottingham.ac.uk>" \
      org.opencontainers.image.title="Correct MALP-EM Map" \
      org.opencontainers.image.description="Corrects a MALP-EM label map by adding a CSF label on unlabelled voxels and on the cerebellar cortex."
