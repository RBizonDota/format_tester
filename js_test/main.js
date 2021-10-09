const fs = require('fs')

function getNanoSecTime() {
  var hrTime = process.hrtime();
  return hrTime[0] + hrTime[1]/1000000000;
}

class ReaderABS{
  constructor(struct_id, capacity, data) {
      this._parse = null
      this._serialize = null
      this.data = data
      this.stat = {
          struct_id:struct_id,
          capacity:capacity,
          serialize:null,
          parse:null,
          over:null
      }
  }

  parse = (data_str)=>{
      var start = getNanoSecTime()
      var data = this._parse(data_str)
      const parse_stop = getNanoSecTime() - start
      this.stat.parse = parse_stop/this.stat.capacity
  }

  serialize = ()=>{
      var start = getNanoSecTime()
      // console.log(this.data.i0, typeof this.data)
      var data_str = this._serialize(this.data)
      const stop = getNanoSecTime() - start
      this.stat.serialize = stop/this.stat.capacity
      this.stat.over = data_str.length/this.stat.capacity
      // console.log(this._serialize, this.data)
      return data_str
  }

  save_stat = (path, test_id)=>{
      var content = test_id+","+this.stat.struct_id+","+this.stat.capacity+","+this.stat.serialize+","+this.stat.parse+","+this.stat.over+"\n"
      fs.appendFileSync(path, content)
  }

  test = (path, test_id) => {
      var data_str = this.serialize()
      // console.log(data_str)
      this.parse(data_str)
      this.save_stat(path, test_id)
  }
}

// JSON
class ReaderJSON extends ReaderABS{
  constructor(struct_id, capacity, data) {
      super(struct_id, capacity, data); 
      this._parse = JSON.parse
      this._serialize = JSON.stringify
  }
}

// XML
const xml_parser = require('xml2json');
var o2x = require('object-to-xml');
var xml_converter = require('xml-js');

class ReaderXML extends ReaderABS{
  constructor(struct_id, capacity, data) {
      super(struct_id, capacity, data); 
      this._parse = (xml)=>{
        try{
          var data = xml_converter.xml2js(xml, { compact: true })
          return data
        }catch(e){
          console.log("Error occured!")
          console.log(this.data)
          console.log(xml)
          console.error(e)
          throw "Error1"
        }
      }
      this._serialize = data=>{
          var xml_str = "<root>"+xml_converter.js2xml(data, { compact: true })+"</root>"
          return xml_str

      } 
  }
}

// YAML
const yaml_parser = require('js-yaml');

class ReaderYAML extends ReaderABS{
  constructor(struct_id, capacity, data) {
      super(struct_id, capacity, data); 
      this._parse = yaml_parser.load
      this._serialize = yaml_parser.dump
  }
}

// TOML
var toml_parser = require('@iarna/toml')
class ReaderTOML extends ReaderABS{
  constructor(struct_id, capacity, data) {
      super(struct_id, capacity, data); 
      this._parse = toml_parser.parse
      this._serialize = toml_parser.stringify
  }
}


// const get_struct = (path)=>{
//     fs.readFile(path, 'utf8' , (err, data_str) => {
//         if (err) {
//           console.error(err)
//           return
//         }
//         data = JSON.parse(data_str)
//         return data
//       })
// }

// const get_dir = (dir)=>fs.readdir(dir, (err, files) => {
//     if (err){
//         console.log("ERROR: error while getting forlders")
//         return
//     }
//     return files
//   });

const CONFIG_FILE = "/etc/format_tester/js_conf.json"
let config_struct = JSON.parse(fs.readFileSync(CONFIG_FILE, {encoding:'utf8', flag:'r'}))

const BATCH = config_struct.batch

const NUM_OF_ITERATIONS = config_struct.n_iterations

const STRUCT_DIR = config_struct.struct_dir+BATCH
const STATS_DIR = config_struct.stat_dir

const DTYPES = config_struct.dtypes

const DTYPE_CONFIG = {
  'json': ReaderJSON,
  'xml': ReaderXML,
  'yaml': ReaderYAML,
  'toml': ReaderTOML,
}

// ЗАПУСКАЕМЫЙ КОД

file_names = fs.readdirSync(STRUCT_DIR)

DTYPES.forEach(dtype_name=>{
  console.log("//-------------------------- "+dtype_name+" ------------------------------------")
  // Сохранение заголовка файла статистики
  var stat_file = STATS_DIR+"js_"+dtype_name+"_"+BATCH+"_"+NUM_OF_ITERATIONS+".csv"
  var csv_header = ",struct_id,capacity,serialize,parse,over\n"

  fs.writeFileSync(stat_file, csv_header)

  // Перебор структур
  var pos = 0
  file_names.forEach(file => {
    var struct_id = parseInt(file.split('_')[0])
    var capacity = parseInt(file.split('_')[1])
    // console.log(struct_id, capacity)
    if (pos%1000 == 0){
      console.log(" ", dtype_name, pos)
    }
    let data_struct = JSON.parse(fs.readFileSync(STRUCT_DIR+"/"+file, {encoding:'utf8', flag:'r'}))
    // console.log(data_struct)

    var parser = new DTYPE_CONFIG[dtype_name](struct_id, capacity, data_struct)
    // console.log(struct)
    for (step = 0; step < NUM_OF_ITERATIONS; step++) {
      parser.test(stat_file, pos)
      pos++;
    }
  });
})
// const data = get_struct()