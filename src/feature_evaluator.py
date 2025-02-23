from agent import Agent

def feature_rater(system_message, target_message):
    rater = Agent(temperature = 0)
    rater.load_system_message(system_message) # "Given a message, rate anger from 1(no anger) to 5(extreme anger)."
    rater.load_message([{"role": "user", "content": target_message}])
    default_schema = {
        "name": "rater_schema",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "rating": {
                    "type": "integer",
                    "description": "Your rating based on the given message.",
                    "enum": [
                        1,
                        2,
                        3,
                        4,
                        5
                    ]
                },
                # response placeholder
            },
            "required": [
                "rating"
            ],
            "additionalProperties": False
        }
    }
    response = rater.get_response(response_format = {"type": "json_schema", "json_schema":default_schema})
    return response['rating']
