package main

import "io"
import "os"
import "path"
import "strings"
import "io/ioutil"
import "encoding/json"
import "text/template"

import "github.com/spf13/pflag"
import log "github.com/sirupsen/logrus"

func main() {
	argTemplate := pflag.StringP("template", "t", "-", "A configuration template")
	argOutput := pflag.StringP("output", "o", "-", "A path to write the rendered configuration to")

	argEnv := pflag.StringSliceP("env", "e", []string{}, "One or more environment variable to load (default: load the complete environment)")
	argFile := pflag.StringSliceP("file", "f", []string{}, "One or more file to load as text")
	argJson := pflag.StringSliceP("json", "j", []string{}, "One or more JSON file to load as an object each")

	argDebug := pflag.BoolP("debug", "d", false, "Enable debug mode")

	pflag.Parse()

	if *argDebug {
		log.SetLevel(log.DebugLevel)
	}

	log.Debug("Args:")
	log.Debug("  Template = ", *argTemplate)
	log.Debug("  Output = ")
	log.Debug("  Env = ", *argEnv)
	log.Debug("  File = ", *argFile)
	log.Debug("  Json = ")
	log.Debug("  Debug = ", *argDebug)

	templateEnvironment := make(map[string]interface{})

	// Environment variables
	envEnvironment := make(map[string]string)
	if len(*argEnv) > 0 {

		for _, name := range *argEnv {
			envValue, ok := os.LookupEnv(name)
			if ok {
				envEnvironment[name] = envValue
			}
		}

	} else {
		for _, name := range os.Environ() {
			envEnvironment[name] = os.Getenv(name)
		}
	}
	templateEnvironment["env"] = envEnvironment

	// Files
	filesEnvironment := make(map[string]string)
	if len(*argFile) > 0 {
		for _, filename := range *argFile {
			keyName := path.Base(filename)
			keyName = strings.Replace(keyName, ".", "_", -1)
			data, err := ioutil.ReadFile(filename)
			if err != nil {
        log.Warningf("Unable to read file '%s': %s", filename, err)
				continue
			}
			filesEnvironment[keyName] = string(data)
		}
	}
	templateEnvironment["file"] = filesEnvironment

	// JSON
	jsonEnvironment := make(map[string]interface{})
	if len(*argJson) > 0 {
		for _, filename := range *argJson {
			keyName := path.Base(filename)
			keyName = strings.Replace(keyName, ".", "_", -1)
			data, err := ioutil.ReadFile(filename)
			if err != nil {
				log.Warningf("Unable to read JSON file '%s': %s", filename, err)
				continue
			}
			var parsedData map[string]interface{}
			err = json.Unmarshal(data, &parsedData)
			if err != nil {
        log.Warningf("Unable to parse JSON file '%s': %s", filename, err)
				continue
			}
			jsonEnvironment[keyName] = parsedData
		}
	}
	templateEnvironment["json"] = jsonEnvironment

	log.Debug("Template Environment: ", templateEnvironment)

	var templateFile io.Reader
	if *argTemplate == "-" {
		templateFile = os.Stdin
	} else {
		var err error
		templateFile, err = os.Open(*argTemplate)
		if err != nil {
			log.Fatal("Unable to open template: ", err)
		}
	}
	templateData, err := ioutil.ReadAll(templateFile)
	if err != nil {
		log.Fatal("Unable to read template: ", err)
	}
	template, _ := template.New(*argTemplate).Parse(string(templateData))
	var outputFile io.Writer
	if *argOutput == "-" {
		outputFile = os.Stdout
	} else {
		var err error
		outputFile, err = os.Create(*argOutput)
		if err != nil {
			log.Fatal("Unable to open output: ", err)
		}
	}
	template.Execute(outputFile, templateEnvironment)
  log.Info("Configuration template rendered")
}
