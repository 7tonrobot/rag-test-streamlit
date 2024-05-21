import boto3
from botocore.exceptions import ClientError

def invoke_agent(agent_id, agent_alias_id, session_id, prompt):
    try:
        client = boto3.session.Session().client(service_name="bedrock-agent-runtime")
        # See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_agent.html
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            enableTrace=True,
            sessionId=session_id,
            inputText=prompt,
        )

        output_text = ""
        trace = {}

        for event in response.get("completion"):
            # Combine the chunks to get the output text
            if "chunk" in event:
                chunk = event["chunk"]
                output_text += chunk["bytes"].decode()

            # Extract trace information from all events
            if "trace" in event:
                for trace_type in ["preProcessingTrace", "orchestrationTrace", "postProcessingTrace"]:
                    if trace_type in event["trace"]["trace"]:
                        if trace_type not in trace:
                            trace[trace_type] = []
                        trace[trace_type].append(event["trace"]["trace"][trace_type])

            # TODO: handle citations/references

    except ClientError as e:
        raise

    return {
        "output_text": output_text,
        "trace": trace
    }
