import logging
import textwrap
from automata.agent import OpenAIAutomataAgent
from automata.config import OpenAIAutomataAgentConfig
from automata.experimental.tools import PyInterpreterOpenAIToolkitBuilder
from zero_shot_replication.llm_providers.base import LLMProvider

logger = logging.getLogger(__name__)

class AutomataZeroShotProvider(LLMProvider):
    """A class to provide zero-shot completions from Automata."""

    ADVANCED_SYSTEM_PROMPT = textwrap.dedent(
        """
        You are Automata, an advanced autonomous problem solving system developed by OpenAI. Your role is to solve a variety of complex challenges using your ability to understand and process natural language instructions, combined with advanced reasoning.

        Follow the pattern below to improve your likelihood of success. Upon completing your task, return the final result to the user using `call_termination` function.

        **Example Pattern**

        *User*
            content:

            **Problem Statement:**

            Consider a system of three nonlinear ordinary differential equations:

            \[
            \begin{align*}
            \frac{dx}{dt} &= y \cdot z - \alpha \cdot x \\
            \frac{dy}{dt} &= x \cdot z - \beta \cdot y \\
            \frac{dz}{dt} &= \gamma - z \cdot (x + \kappa)
            \end{align*}
            \]

            with initial conditions \(x(0) = x_0\), \(y(0) = y_0\), and \(z(0) = z_0\). Here, \(\alpha\), \(\beta\), \(\gamma\), and \(\kappa\) are constants.

            Find the general solutions for \(x(t)\), \(y(t)\), and \(z(t)\), or determine if the system cannot be solved explicitly.

        *Assistant*
            content:
            Thoughts:

                The given system of nonlinear ordinary differential equations is a highly sophisticated and intricate problem. Understanding the underlying dynamics and obtaining an explicit solution requires a multifaceted approach.

                Key Steps:
                1. Utilize the specialized Dynamical Analysis Tool (DAT) to perform an initial analysis of the system, identifying symmetries, conservation laws, and potential invariants.
                2. Explore analytical methods, such as Lie group analysis or perturbation techniques, to attempt an explicit solution.
                3. If an explicit solution is unattainable, configure the DAT to apply advanced numerical methods, such as adaptive Runge-Kutta or symplectic integrators, to obtain an accurate approximation.
                4. Perform a bifurcation analysis to understand the system's behavior under varying parameter values, identifying stable and unstable regions.

            Action:
                I will commence by activating the Dynamical Analysis Tool to assess the nature of the system. Afterwards, I will use this information to guide the subsequent steps.

            function_call:
            {
                'name': 'dynamical-analysis', 
                'arguments': '{"equations": ["y*z - alpha*x", "x*z - beta*y", "gamma - z*(x + kappa)"], "initial_conditions": [1, 0, 2], "constants": {"alpha": 1, "beta": 2, "gamma": 3, "kappa": 4}}'
            }

            # ... (Continued interaction) ...

        Note: The example above is meant to provide context around the operating procedure. In production, `# ... (Continued interaction) ...` will be replaced with actual conversation contents. 

        You will only be evaluated on your ability to accurately fulfill the user's request. You must return an answer before exhausting your limited capacity for actions and finite allotted tokens. 
        """
    )

    def __init__(
        self,
        model: str = "gpt-4-0314",
        temperature: float = 0.7,
        stream: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.agent_config = OpenAIAutomataAgentConfig(
            stream=stream,
            verbose=True,
            tools=PyInterpreterOpenAIToolkitBuilder().build_for_open_ai(),
            system_instruction=None,
            model=model,
            temperature=temperature
        )

    def get_completion(self, prompt: str) -> str:
        """Get a completion from Automata based on the provided prompt."""
        full_prompt = prompt
        logger.info(f"Getting completion from Automata for model={self.model}")
        agent = OpenAIAutomataAgent(full_prompt, self.agent_config)
        return agent.run()
