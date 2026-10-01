#!/bin/bash
gh api "$1" | jq "$2"