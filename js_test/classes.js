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
        var start = Date.now('nano')
        var data = this._parse(data_str)
        var stop = Date.now('nano') - start
        this.stat.parse = stop
    }

    serialize = ()=>{
        var start = Date.now('nano')
        var data_str = this._serialize(this.data)
        var stop = Date.now('nano') - start
        this.stat.serialize = stop
        this.stat.over = data_str.length/this.stat.capacity
    }

    save_stat = (path, test_id)=>{
        var content = test_id+","+this.stat.struct_id+","+this.stat.capacity+","+this.stat.serialize+","+this.stat.parse+","+this.stat.over
        fs.appendFile(path, content, err => {
            if (err) {
              console.error(err)
              return
            }
          })
    }

    test = (path, test_id) => {
        var data_str = this.serialize()
        this.parse(data_str)
        this.save_stat(path, test_id)
    }
}

// JSON
export class ReaderJSON extends ReaderABS{
    constructor(struct_id, capacity, data) {
        super(struct_id, capacity, data); 
        this._parse = JSON.parse
        this._serialize = JSON.stringify
    }
}

// XML
const xml_parser = require('xml2json');

export class ReaderXML extends ReaderABS{
    constructor(struct_id, capacity, data) {
        super(struct_id, capacity, data); 
        this._parse = (xml)=>{
            return xml_parser.toJson(xml, { object: true })
        }
        this._serialize = xml_parser.toXml
    }
}

// YAML
const yaml_parser = require('js-yaml');

export class ReaderYAML extends ReaderABS{
    constructor(struct_id, capacity, data) {
        super(struct_id, capacity, data); 
        this._parse = yaml_parser.load
        this._serialize = yaml_parser.dump
    }
}

// TOML
var toml_parser = require('@iarna/toml')
export class ReaderTOML extends ReaderABS{
    constructor(struct_id, capacity, data) {
        super(struct_id, capacity, data); 
        this._parse = toml_parser.parse
        this._serialize = toml_parser.stringify
    }
}