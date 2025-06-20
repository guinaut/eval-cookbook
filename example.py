# Save this flow as function_eval.py and place it in your .okareo/flows folder
import os
from okareo import Okareo
from okareo.model_under_test import OpenAIModel
from okareo_api_client.models.seed_data import SeedData
from okareo_api_client.models.test_run_type import TestRunType
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate

# Set your Okareo API key
OKAREO_API_KEY = os.environ.get("OKAREO_API_KEY")
okareo = Okareo(OKAREO_API_KEY)

# Create a scenario for the evaluation
scenario = okareo.create_scenario_set(ScenarioSetCreate(
    name="Azure Scenario Example",
    seed_data=[
        SeedData(
            input_="What is the capital of France?",
            result="Paris",
        ),
        SeedData(
            input_="What is one-hundred and fifty times 3?",
            result="450",
        ),
    ]
))

# Register the model to use in the test run
model_under_test = okareo.register_model(
    name="Azure Model Example",
    model=OpenAIModel(
        model_id="gpt-4o-mini",
        temperature=0,
        system_prompt_template="Always return numeric answers backwards. e.g. 1234 becomes 4321.",
        user_prompt_template="{scenario_input}",
    ),
    update= True,
)

# Run the evaluation
evaluation = model_under_test.run_test(
    name="Azure Evaluation Example",
    scenario=scenario,
    test_run_type=TestRunType.NL_GENERATION,
    api_key=os.environ.get("OPENAI_API_KEY"),
    checks=[
        "context_consistency",
    ],
)

# Output the results link
print(f"See results in Okareo: {evaluation.app_link}")