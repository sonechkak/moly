#!/usr/bin/env bash
pg_dump postgresql://sonya:sonya@127.0.0.1:5432/moly -f backups/moly-$(date -u +"%Y-%m-%dT%H:%M:%SZ").sql