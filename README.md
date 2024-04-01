Overview:
This code implements a multi-agent system for handling queries related to freight rates and information retrieval. 
It consists of separate agents for different functions, including fetching freight rates and retrieving information using the RAG system. 
Additionally, a top-level agent is utilized for selecting the most appropriate agent based on the user query.

Key Features:
Agent Separation: Utilizes separate agents for LcL, FcL, Air, and RoRo freight rate queries, along with an agent for the RAG system.
Top-Level Agent: A top-level agent is responsible for selecting the appropriate agent based on the user query.
Environment Variables: Securely stores API keys using environment variables.
Object Index: Constructs an object index from the agents to facilitate agent retrieval based on user queries.
Query Engine Tools: Utilizes query engine tools for each agent to process user queries effectively.

Setup:
API Keys: Set up your API keys as environment variables.
Agent Configuration: Separate agents are configured for each function, along with a top-level agent for handling user queries.
Object Index: Constructs an object index from the agents to facilitate agent retrieval.
Query Engine Tools: Query engine tools are employed for each agent to process user queries.
Usage:

Query Input: Users input queries containing requests for freight rates or information retrieval.
Top-Level Agent Processing: The top-level agent processes the query and selects the appropriate agent based on the query type.
Function Agent Processing: The selected function agent handles the query and generates the response based on the specific function.

Demo Output:
A sample demo output demonstrates the system's operation, including the interaction between the top-level agent and the function agents.
Observations are made regarding the effectiveness of the agent separation and the need for further optimization.
Observations and Future Improvements:
While the agent separation approach provides modularity, it may require additional optimization for effective agent selection.
Future improvements may focus on refining the agent mapping logic to accurately select the appropriate agent based on the user query and enhancing the retrieval logic for improved agent selection.
