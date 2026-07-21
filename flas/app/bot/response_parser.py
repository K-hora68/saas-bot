import json
import re


class ResponseParser:

    def parse(self, response: dict) -> dict:

        raw_response = response.get(
            "response",
            ""
        )

        # Remove markdown code blocks
        raw_response = re.sub(
            r"```json|```",
            "",
            raw_response
        ).strip()


        try:
            data = json.loads(raw_response)

            return {
                "reply": data.get("reply", ""),
                "media": data.get("media", []),
                "follow_up": data.get("follow_up", "")
            }

        except json.JSONDecodeError as e:

            print("JSON ERROR:", e)
            print("RAW RESPONSE:", raw_response)

            return {
                "reply": raw_response,
                "media": [],
                "follow_up": ""
            }