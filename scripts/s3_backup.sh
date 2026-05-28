#!/usr/bin/env bash
set -euo pipefail

BACKUP_SOURCE="${BACKUP_SOURCE:-/app/data}"
BACKUP_BUCKET="${BACKUP_BUCKET:-asir-backups-<tu-nombre>}"
BACKUP_PREFIX="${BACKUP_PREFIX:-backups}"
WORKDIR="${WORKDIR:-/tmp/asir-backups}"
DATE="$(date +%Y-%m-%d)"
TIMESTAMP="$(date +%Y-%m-%d_%H-%M-%S)"
ARCHIVE="${WORKDIR}/backup-${TIMESTAMP}.tar.gz"

mkdir -p "${WORKDIR}"

if [ ! -d "${BACKUP_SOURCE}" ]; then
  echo "Backup source does not exist: ${BACKUP_SOURCE}" >&2
  exit 1
fi

tar -czf "${ARCHIVE}" -C "$(dirname "${BACKUP_SOURCE}")" "$(basename "${BACKUP_SOURCE}")"
aws s3 cp "${ARCHIVE}" "s3://${BACKUP_BUCKET}/${BACKUP_PREFIX}/${DATE}/$(basename "${ARCHIVE}")"
rm -f "${ARCHIVE}"

echo "Backup uploaded to s3://${BACKUP_BUCKET}/${BACKUP_PREFIX}/${DATE}/"
