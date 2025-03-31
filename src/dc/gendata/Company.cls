Class dc.gendata.Company Extends %Persistent
{

/// Company name
Property CompanyName As %String;

/// Company name
Property CompanyAddress As %String;

/// Company name
Property CompanyPhone As %String;

/// Company name
Property CompanyContactName As %String;

/// Add a sample initial data
ClassMethod AddInitialData() As %Status
{
    Set sc = $$$OK
    Set Company = ##class(Company).%New()
    Set Company.CompanyAddress = "Memorial Street, 12"
    Set Company.CompanyContactName = "Jack Mills"
    Set Company.CompanyName = "Acme Co"
    Set Company.CompanyPhone = "251 555-1212"
    Return Company.%Save()
}

Storage Default
{
<Data name="CompanyDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>CompanyName</Value>
</Value>
<Value name="3">
<Value>CompanyAddress</Value>
</Value>
<Value name="4">
<Value>CompanyPhone</Value>
</Value>
<Value name="5">
<Value>CompanyContactName</Value>
</Value>
</Data>
<DataLocation>^dc.gendata.CompanyD</DataLocation>
<DefaultData>CompanyDefaultData</DefaultData>
<IdLocation>^dc.gendata.CompanyD</IdLocation>
<IndexLocation>^dc.gendata.CompanyI</IndexLocation>
<StreamLocation>^dc.gendata.CompanyS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
