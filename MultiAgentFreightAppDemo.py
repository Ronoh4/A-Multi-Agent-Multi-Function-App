# Import relevant classes from correct modules 
import requests
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.objects import ObjectIndex, SimpleToolNodeMapping
from llama_index.agent.openai_legacy import FnRetrieverOpenAIAgent
import os

# Set environmental variables
os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxZ7M"
openai_api_key = os.environ["OPENAI_API_KEY"]

                    #Define 5 separate functions for the 4 API calls and 1 RAG system

# Define Function 1 for LcL API Call

def fetch_LcL_freight_rates(origin, destination, cargo_weight, cargo_type, weight, length, width, height, units):
    url = f"yourendpoint?origin={origin}&destination={destination}&cargoWeight={cargo_weight}&cargoType={cargo_type}&weight={weight}&length={length}&width={width}&height={height}&units={units}"
    response = requests.get(url)
    print("Request made")

    if response.ok:
        try:
            data = response.json()
            print("Response obtained")

            LcL_quote_details = []

            relevant_shipments = [
                quote for quote in data
                ]

            if relevant_shipments:
                print("LcL quote details:")
                for shipment in relevant_shipments:
                    shipment_dict = {
                        "quoteId": shipment["quoteId"],
                        "countryOfOrigin": shipment["countryOfOrigin"],
                        "portOfOrigin": shipment["portOfOrigin"],
                        "portOfOriginCode": shipment["portOfOriginCode"],
                        "countryOfDestination": shipment["countryOfDestination"],
                        "portOfDestination": shipment["portOfDestination"],
                        "portOfDestinationCode": shipment["portOfDestinationCode"],
                        "carrier": shipment["carrier"],
                        "rate": shipment["generalCargo"] if shipment["generalCargo"] else shipment["hazardousCargo"],
                        "validFrom": shipment["validFrom"],
                        "validTo": shipment["validTo"],
                        "terms": shipment["terms"],
                        "bookingLink": shipment["bookingLink"]
                    }
                    LcL_quote_details.append(shipment_dict)
                return LcL_quote_details
            else:
                print("No relevant shipments found.")
        except ValueError: 
            print(f"Response is not JSON. Response content: {response.text}")
    else:
        print(f"Error fetching data. Status code: {response.status_code}. Response content: {response.text}")

LcL_freight_quote = fetch_LcL_freight_rates("china", "kenya", 100, "general", 100, 10, 10, 10, "inches")

# Define Function 2 for FcL API Call

def fetch_FcL_freight_rates(origin, destination, container_type, number_of_containers):
    url = f"yourendpoint?origin={origin}&destination={destination}&containerType={container_type}&numberOfContainers={number_of_containers}"
    response = requests.get(url)
    print("Request made")

    if response.ok:
        try:
            data = response.json()
            print("Response obtained")

            FcL_quote_details = []
        
            relevant_shipments = [
                quote for quote in data
                ]

            if relevant_shipments:
                print("FcL quote details:")
                for shipment in relevant_shipments:
                    shipment_dict = {
                        "quoteId": shipment["quoteId"],
                        "countryOfOrigin": shipment["countryOfOrigin"],
                        "portOfOrigin": shipment["portOfOrigin"],
                        "portOfOriginCode": shipment["portOfOriginCode"],
                        "countryOfDestination": shipment["countryOfDestination"],
                        "portOfDestination": shipment["portOfDestination"],
                        "portOfDestinationCode": shipment["portOfDestinationCode"],
                        "carrier": shipment["carrier"],
                        "validFrom": shipment["validFrom"],
                        "validTo": shipment["validTo"],
                        "terms": shipment["terms"],
                        "bookingLink": shipment["bookingLink"]
                    }
                    FcL_quote_details.append(shipment_dict)
                return FcL_quote_details
            else:
                print("No relevant shipments found.")
        except ValueError: 
            print(f"Response is not JSON. Response content: {response.text}")
    else:
        print(f"Error fetching data. Status code: {response.status_code}. Response content: {response.text}")

FcL_freight_quote = fetch_FcL_freight_rates("china", "kenya", "20GP", 1)

# Define Function 3 for Air Freight API Call

def fetch_air_freight_rates(origin, destination, cargo_weight, cargo_type, length, width, height, units):
    url = f"yourendpoint?origin={origin}&destination={destination}&cargoWeight={cargo_weight}&cargoType={cargo_type}&length={length}&width={width}&height={height}&units={units}"
    response = requests.get(url)
    print("Request made")

    if response.ok:
        try:
            data = response.json()
            print("Response obtained")

            Air_quote_details = []

            relevant_shipments = [
                quote for quote in data
                ]

            if relevant_shipments:
                print("Air quote details:")
                for shipment in relevant_shipments:
                    shipment_dict = {
                        "quoteId": shipment["quoteId"],
                        "countryOfOrigin": shipment["countryOfOrigin"],
                        "originCityAirport": shipment["originCityAirport"],
                        "airportOfLoading": shipment["airportOfLoading"],
                        "airportOfOriginCode": shipment["airportOfOriginCode"],
                        "countryOfDestination": shipment["countryOfDestination"],
                        "destinationCityAirport": shipment["destinationCityAirport"],
                        "airportOfDischarge": shipment["airportOfDischarge"],
                        "airportOfDischargeCode": shipment["airportOfDischargeCode"],
                        "cargoType": shipment["cargoType"],
                        "carrier": shipment["carrier"],
                        "carrierCode": shipment["carrierCode"],
                        "travelTime": shipment["travelTime"],
                        "offerValidUntil": shipment["offerValidUntil"],
                        "termsConditions": shipment["termsConditions"],
                        "bookingLink": shipment["bookingLink"]
                    }
                    Air_quote_details.append(shipment_dict)
                return Air_quote_details
            else:
                print("No relevant shipments found.")
        except ValueError: 
            print(f"Response is not JSON. Response content: {response.text}")
    else:
        print(f"Error fetching data. Status code: {response.status_code}. Response content: {response.text}")

air_freight_quote = fetch_air_freight_rates("usa", "kenya", 100, "general", 10, 10, 10, "inches")


# Define Function 4 for RoRo Freight API Call

def fetch_RoRo_freight_rates(origin, destination, manufacturer, model, vehicle_type, fuel_type, weight, drive_type):
    url = f"yourendpoint?origin={origin}&destination={destination}&manufacturer={manufacturer}&model={model}&vehicleType={vehicle_type}&fuelType={fuel_type}&weight={weight}&driveType={drive_type}"
    response = requests.get(url)
    print("Request made")

    if response.ok:
        try:
            data = response.json()
            print("Response obtained")

            RoRo_quote_details = []

            relevant_shipments = [
                shipment for shipment in data
            ]

            if relevant_shipments:
                print("RoRo Freight rates quote:")
                for shipment in relevant_shipments:
                    shipment_dict = {
                        "quoteId": shipment["quoteId"],
                        "countryOfOrigin": shipment["countryOfOrigin"],
                        "portOfOrigin": shipment["portOfOrigin"],
                        "portOfOriginCode": shipment["portOfOriginCode"],
                        "countryOfDestination": shipment["countryOfDestination"],
                        "portOfDestination": shipment["portOfDestination"],
                        "portOfDestinationCode": shipment["portOfDestinationCode"],
                        "carrier": shipment["carrier"],
                        "validFrom": shipment["validFrom"],
                        "validTo": shipment["validTo"],
                        "terms": shipment["terms"],
                        "bookingLink": shipment["bookingLink"]
                    }
                    RoRo_quote_details.append(shipment_dict)
                return RoRo_quote_details
            else:
                print("No relevant shipments found.")
        except ValueError: 
            print(f"Response is not JSON. Response content: {response.text}")
    else:
        print(f"Error fetching data. Status code: {response.status_code}. Response content: {response.text}")

RoRo_freight_quote = fetch_RoRo_freight_rates("japan", "kenya", "audi", "a5", "coupe", "petrol", 1400, "2wd")

# Define Function 5 for RAG System Call

def get_rag_response(query):
    parser = LlamaParse(
        api_key="llx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxGh7",
        result_type="text",
        language="en",
        varbose=True
    )

    documents = parser.load_data("C:\\Users\\user\\Documents\\Jan 2024\\Projects\\RAGs\\Files\\VehicleImport.pdf")

    index = VectorStoreIndex.from_documents(documents)

    index.set_index_id("vector_index")
    index.storage_context.persist("./storage")

    storage_context = StorageContext.from_defaults(persist_dir="storage")

    index = load_index_from_storage(storage_context, index_id="vector_index")

    query_engine = index.as_query_engine(response_mode="tree_summarize")
    response = query_engine.query("What is the age restriction for car that can be imported into Kenya?")
    return response

# Set up Function tools for each of the 5 Functions
LcL_freight_tool = FunctionTool.from_defaults(fn=fetch_LcL_freight_rates) 
FcL_freight_tool = FunctionTool.from_defaults(fn=fetch_FcL_freight_rates)
Air_freight_tool = FunctionTool.from_defaults(fn=fetch_air_freight_rates)
RoRo_freight_tool = FunctionTool.from_defaults(fn=fetch_RoRo_freight_rates)
rag_tool = FunctionTool.from_defaults(fn=get_rag_response)

# Set up LLM instance for agents to use
openai_key ="sk-gUxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxOZ7M"
llm = OpenAI(api_key=openai_key, model = "gpt-3.5-turbo")

# Create separate agents for each function
LcL_agent = OpenAIAgent.from_tools(
    [LcL_freight_tool],
    llm=llm,
    verbose=True,
    system_prompt=f"""\
You are a specialized agent designed to provide LcL freight rates.
You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
""",
)
FcL_agent = OpenAIAgent.from_tools(
    [FcL_freight_tool],
    llm=llm,
    verbose=True,
    system_prompt=f"""\
You are a specialized agent designed to provide FcL freight rates.
You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
""",
)
Air_agent = OpenAIAgent.from_tools(
    [Air_freight_tool],
    llm=llm,
    verbose=True,
    system_prompt=f"""\
You are a specialized agent designed to provide air freight rates.
You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
""",
)
RoRo_agent = OpenAIAgent.from_tools(
    [RoRo_freight_tool],
    llm=llm,
    verbose=True,
    system_prompt=f"""\
You are a specialized agent designed to provide RoRo freight rates.
You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
""",
)
rag_agent = OpenAIAgent.from_tools(
    [rag_tool],
    llm=llm,
    verbose=True,
    system_prompt=f"""\
You are a specialized agent designed to provide RAG system responses.
You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
""",
)

# Create agent dictionary
agents = {
    "LcL_agent": LcL_agent,
    "FcL_agent": FcL_agent,
    "Air_agent": Air_agent,
    "RoRo_agent": RoRo_agent,
    "rag_agent": rag_agent,
}

# Define a tool for each function agent
query_engine_tools = []
for agent_name, agent in agents.items():
    tool = QueryEngineTool(
        query_engine=agent,
        metadata=ToolMetadata(
            name=f"tool_{agent_name}",
            description=f"This tool uses the {agent_name} agent to answer queries.",
        ),
    )
    query_engine_tools.append(tool)

# Define a mapping of tools to nodes
tool_mapping = SimpleToolNodeMapping.from_objects(query_engine_tools)

# Create an object index from the tools
obj_index = ObjectIndex.from_objects(
    query_engine_tools,
    tool_mapping,
    VectorStoreIndex,
) 
# Instantiate a retriever over the object index
retriever = obj_index.as_retriever(similarity_top_k=3)

# Create the top-level agent using the retriever
top_agent = FnRetrieverOpenAIAgent.from_retriever(
    retriever,
    system_prompt=""" \
You are a top-level agent designed to choose the most appropriate agent of the 5 agents provided in the object index based on the user query and use the appropriate agent to answer queries about freight and cars.
Please ALWAYS choose the approprate agents among the 5 provided based on the user query to answer a question. Do NOT rely on prior knowledge.\

""",
    verbose=True,
)

# Query the top agent for freight rates
response = top_agent.query("What is the age restriction for car that can be imported into Kenya?")
print("Final response:")
print(response)



# Demo output

#STARTING TURN 1
#---------------

#=== Calling Function ===
#Calling function: tool_RoRo_agent with args: {"input":"What is the age restriction for car that can be imported into Kenya?"}
#Added user message to memory: What is the age restriction for car that can be imported into Kenya?
#=== Calling Function ===
#Calling function: fetch_RoRo_freight_rates with args: {"destination":"Kenya"}
#Got output: Error: fetch_RoRo_freight_rates() missing 7 required positional arguments: 'origin', 'manufacturer', 'model', 'vehicle_type', 'fuel_type', 'weight', and 'drive_type'
#========================

#Got output: I need more specific details about the car you are looking to import into Kenya in order to provide information on the age restriction. 
#Could you please provide me with the manufacturer, model, vehicle type, fuel type, weight, and drive type of the car you are interested in importing? 
#This information will help me retrieve the necessary details for you.
#========================

#STARTING TURN 2

#Final response:
#I need more specific details about the car you are looking to import into Kenya in order to provide information on the age restriction. 
#Could you please provide me with the manufacturer, model, vehicle type, fuel type, weight, and drive type of the car you are interested in importing? 
#This information will help me retrieve the necessary details for you.


# My observations
# Separating agents for each functions and using a top-level agent for appropriate agent retrieval proved ineffective 
# and seems to need additional optimizations including Agent Mapping to map specific query types to corresponding agents,
# and retrieval Logic optimizations to enhance the retriever's logic to analyze the user query and select the appropriate agent based on the mapping. 
# In production, I anticipate it would require several iterations to refine the retrieval logic and mapping agents to ensure the top-level agent
# accurately selects the appropriate agent to handle each user query.