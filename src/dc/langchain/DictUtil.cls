Class dc.langchain.DictUtil Extends %RegisteredObject
{

ClassMethod ClassInfo()
{
        #dim ex As %Exception.AbstractException
        try {
            set currentNS=$NAMESPACE
            while (1) {
                read "Please specify namespace: ",x
                if x'=""  quit
            }
            set $NAMESPACE=x 
            write !!
            Set statement = ##class(%SQL.Statement).%New()
            Do statement.%PrepareClassQuery("%Dictionary.ClassDefinitionQuery","Summary")
            set rs = statement.%Execute()
            while rs.%Next() {
                set name=rs.%Get("Name")
                if name["%" continue            // Skip the class with % in the name
                if $extract(name,1,3)="csp" continue  // skip csp.*
                if $extract(name,1,3)="csr" continue  // skip csr.*
                write name,!
            }
            set $NAMESPACE=currentNS
        }
        catch ex {
            write "Error occured: ",ex.DisplayString(),!
            set $NAMESPACE=$get(currentNS)
        }
}

}
