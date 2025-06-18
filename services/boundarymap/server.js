const express = require('express')
const app = express()
const port = 8384
const fs = require('fs');

app.use(express.static('public'))
app.use(express.json())


app.get('/', (req,res)=> {
    res.status(200).send()
})

app.post('/', (req,res)=> {
    const {parcel} = req.body
    if(!parcel){
        return res.status(400).send({status: 'failed'})
    }
    res.status(200).send({status: 'recieved'})
    console.log(parcel)
  
    var temp=[]
    for(i=0;i<parcel.slice(0,-1).length; i++){
        temp.push([parcel[i][1],parcel[i][0],30])
    }
    var csv = temp
    .map((item) => {
     
      // Here item refers to a row in that 2D array
      var row = item;
       
      // Now join the elements of row with "," using join function
      return row.join(",");
    }) // At this point we have an array of strings
    .join("\n");
   
    fs.writeFileSync('coords.csv', csv);

})


app.listen(port, () => console.log('Server started on port 8384'))
