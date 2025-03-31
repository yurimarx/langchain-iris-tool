Class dc.gendata.FakeData Extends %Persistent
{

/// Generate fake data using Generative AI
ClassMethod Generate(schema As %String, table As %String, filter As %String, topic As %String, amount As %Integer, extra As %String, Output results As %String) As %Status
{
        
        Set sc = $$$OK
        
        set samples = []

        set tStatement = ##class(%SQL.Statement).%New()
        set query = 
                "SELECT * "_
                "  FROM  "_schema_"."_table_
                " WHERE "_filter
        set sc = tStatement.%Prepare(query)
        
        if sc'=1 {write "%Prepare failed:" do $System.Status.DisplayError(sc) quit} 

        set rows = tStatement.%Execute()
        
        while rows.%Next() {
            set sampleObj = {}
            set currentCol = 1
            set sample = ""
            
            While tStatement.%Metadata.columns.GetAt(currentCol) {
                set column = tStatement.%Metadata.columns.GetAt(currentCol)
                set sample = sample_column.colName_": "_rows.%Get(column.colName)
                If currentCol < tStatement.%Metadata.columns.Count() {
                    set sample = sample_", " 
                }
                set currentCol = currentCol + 1
            }

            set sampleObj.example = sample

            Do samples.%Push(sampleObj)
            
        }

        write "Sample data:"_samples.%ToJSON(),!
        write "The generation process will take a few minutes (10-30 minutes)",!
        
        Try {
            set results = ..DoFakeGenerate(samples.%ToJSON(), topic, amount, extra)
        } Catch ex {
            Set sc=ex.AsStatus()
        } 

        Write "Check results on the output variable passed", !

        Return sc
}

ClassMethod DoFakeGenerate(sample As %String, topic As %String, amount As %Integer, extra As %String) [ Language = python ]
{
    import json
    from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
    from langchain_experimental.tabular_synthetic_data.base import SyntheticDataGenerator
    from langchain_experimental.tabular_synthetic_data.prompts import (
        SYNTHETIC_FEW_SHOT_PREFIX,
        SYNTHETIC_FEW_SHOT_SUFFIX,
    )
    from langchain_community.llms import Ollama
    from langchain_community.chat_models import ChatOllama
    from dotenv import load_dotenv
    import time

    llm = ChatOllama(model="mistral", temperature=0.7, base_url="http://ollama:11434")

    OLLAMA_TEMPLATE = PromptTemplate.from_template(template="{example}")

    prompt_template = FewShotPromptTemplate(
        prefix=SYNTHETIC_FEW_SHOT_PREFIX,
        examples=json.loads(sample),
        suffix=SYNTHETIC_FEW_SHOT_SUFFIX, 
        input_variables=["subject", "extra"],
        example_prompt=OLLAMA_TEMPLATE,
    )

    generator = SyntheticDataGenerator(template=prompt_template, llm=llm)

    results = generator.generate(subject=topic, runs=amount, extra=extra)

    return json.dumps(results)
}

Storage Default
{
<Data name="FakeDataDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
</Data>
<DataLocation>^dc.gendata.FakeDataD</DataLocation>
<DefaultData>FakeDataDefaultData</DefaultData>
<IdLocation>^dc.gendata.FakeDataD</IdLocation>
<IndexLocation>^dc.gendata.FakeDataI</IndexLocation>
<StreamLocation>^dc.gendata.FakeDataS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
