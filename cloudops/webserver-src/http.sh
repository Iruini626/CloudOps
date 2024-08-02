INSTANCE_ID=$(ec2-metadata -i | cut -d " " -f 2)
PORT_80=$(netstat -an | grep 80 | wc -l)
aws cloudwatch put-metric-data --metric-name PORT_80_AVAILABILITY --dimensions Instance=$INSTANCE_ID --namespace "Custom" --value $PORT_80