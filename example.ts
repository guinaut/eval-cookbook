import {
  Okareo,
  OpenAIModel,
  TestRunType,
  GenerationReporter,
} from "okareo-ts-sdk";

const okareo = new Okareo({ api_key: process.env.OKAREO_API_KEY || "" });

const main = async () => {
  try {
    const project_id = "8c69ab40-7e5e-4449-ad8c-f1e271cf62e6"; // Replace with your actual project ID

    // Create the scenario to evaluate the model with
    const scenario = await okareo.create_scenario_set({
      name: "Simple Scenario Example",
      project_id,
      seed_data: [
        {
          input: "What is the capital of France?",
          result: "Paris",
        },
        {
          input: "What is one-hundred and fifty times 3?",
          result: "450",
        },
      ],
    });

    // Register the model under test
    const model_under_test = await okareo.register_model({
      name: "Simple Model Example",
      project_id: project_id,
      models: {
        type: "openai",
        model_id: "gpt-4o-mini",
        temperature: 0,
        system_prompt_template:
          "Always return numeric answers backwards. e.g. 1234 becomes 4321.",
        user_prompt_template: "{scenario_input}",
      } as OpenAIModel,
      update: true,
    });

    // Run the evaluation
    const evaluation = await model_under_test.run_test({
      name: "Simple Example Evaluation",
      project_id,
      scenario_id: scenario.scenario_id,
      model_api_key: process.env.OPENAI_API_KEY || "",
      type: TestRunType.NL_GENERATION,
      calculate_metrics: true,
      checks: ["context_consistency"],
    });

    const reporter = new GenerationReporter({
      eval_run: evaluation,
      pass_rate: {
        context_consistency: 1.0,
      },
    });
    reporter.log();
  } catch (error) {
    console.error(error);
  }
};
main();
