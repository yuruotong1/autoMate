from route.llm import llm_route
from route.code_executor import code_executor_route
from fastapi import FastAPI
import uvicorn
app = FastAPI()

app.include_router(llm_route)
app.include_router(code_executor_route)

if __name__ == "__main__":
    uvicorn.run(app,port=5000)

# additional requirements: fastapi uvicorn