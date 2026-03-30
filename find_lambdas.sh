#!/bin/bash
for R in $(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text); do
    COUNT=$(aws lambda list-functions --region $R --query 'length(Functions)' --output text 2>/dev/null)
    if [ "$COUNT" -gt 0 ] 2>/dev/null; then
        echo "📦 Région $R : $COUNT fonction(s)"
        aws lambda list-functions \
            --region $R \
            --query 'Functions[*].FunctionName' \
            --output text | tr '\t' '\n' | sed 's/^/   → /'
        echo ""
    fi
done
