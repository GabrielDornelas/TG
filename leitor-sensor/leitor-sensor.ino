//Trabalho de Graduação, WebSensor, Gabriel Dornelas
 
#include <ESP8266WiFi.h> //Importa a Biblioteca ESP8266WiFi
const char* SSID = "Dornelas"; //SSID /nome da rede WI-FI que deseja se conectar
const char* PASSWORD = "ArEIAmOlhAdA39562652"; //Senha da rede WI-FI que deseja se conectar
WiFiClient espClient; //Cria o objeto espClient

#include <PubSubClient.h> //Importa a Biblioteca PubSubClient
const char* BROKER_MQTT = "iot.eclipse.org"; //URL do broker MQTT que se deseja utilizar
#define ID_MQTT  "Gabriel" //id mqtt (para identificação de sessão)
int BROKER_PORT = 1883; //Porta do Broker MQTT
PubSubClient MQTT(espClient); //Instancia o Cliente MQTT passando o objeto espClient
#define topicoTemperatura "sensorDornelas/temperatura" //nomeando tópico de temperatura do servidor
#define topicoUmidade "sensorDornelas/umidade" //nomeando tópico de umidade do servidor

// --- DHT ---
#include <DHT.h> //biblioteca para uso do sensor de temperatura/umidade
#define DHTPIN D3 //definição do pino a ser utilizado na placa nodemcu
#define DHTTYPE DHT11 //definição do modelo do sensor a ser utilizado
DHT dht(DHTPIN, DHTTYPE); //função para utilizar o sensor
int umidade; //variável onde será armazenado dado de umidade
int temperatura; //variável onde será armazenado dado de temperatura

#define TOPICO_SUBSCRIBE "sensorDornelas" //tópico MQTT de escuta
//#define TOPICO_PUBLISH "novo" //tópico MQTT de envio de informações para Broker

//defines - mapeamento de pinos do NodeMCU
#define D3
 
//Prototypes
void initSerial();
void initWiFi();
void initMQTT();
void reconectWiFi(); 
void VerificaConexoesWiFIEMQTT(void);
 
//Implementações das funções
void setup() 
{
    //inicializações:
    initSerial();
    initWiFi();
    initMQTT();
}
 
//Função: inicializa comunicação serial com baudrate 115200 (para fins de monitorar no terminal serial o que está acontecendo.
void initSerial() 
{
    Serial.begin(115200);
}
 
//Função: inicializa e conecta-se na rede WI-FI desejada
void initWiFi() 
{
    delay(10);
    Serial.println("------Conexao WI-FI------");
    Serial.print("Conectando-se na rede: ");
    Serial.println(SSID);
    Serial.println("Aguarde");
    
    reconectWiFi();
}
 
//Função: inicializa parâmetros de conexão MQTT(endereço do broker, porta e seta função de callback)
void initMQTT() 
{
    MQTT.setServer(BROKER_MQTT, BROKER_PORT); //informa qual broker e porta deve ser conectado
}
 
//Função: reconecta-se ao broker MQTT (caso ainda não esteja conectado ou em caso de a conexão cair) em caso de sucesso na conexão ou reconexão, o subscribe dos tópicos é refeito.
void reconnectMQTT() 
{
    while (!MQTT.connected()) 
    {
        Serial.print("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) 
        {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            MQTT.subscribe(TOPICO_SUBSCRIBE); 
        } 
        else 
        {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Havera nova tentatica de conexao em 2s");
            delay(2000);
        }
    }
}
 
//Função: reconecta-se ao WiFi
void reconectWiFi() 
{
    //se já está conectado a rede WI-FI, nada é feito. 
    //Caso contrário, são efetuadas tentativas de conexão
    if (WiFi.status() == WL_CONNECTED)
        return;
        
    WiFi.begin(SSID, PASSWORD); // Conecta na rede WI-FI
    
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(100);
        Serial.print(".");
    }
  
    Serial.println();
    Serial.print("Conectado com sucesso na rede ");
    Serial.print(SSID);
    Serial.println("IP obtido: ");
    Serial.println(WiFi.localIP());
}
 
//Função: verifica o estado das conexões WiFI e ao broker MQTT. 
//Em caso de desconexão (qualquer uma das duas), a conexão é refeita.
void VerificaConexoesWiFIEMQTT(void)
{
    if (!MQTT.connected()) 
        reconnectMQTT(); //se não há conexão com o Broker, a conexão é refeita
    
     reconectWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}
 
//Função: envia ao Broker o estado atual do output 
void EnviaEstadoOutputMQTT(void)
{
    Serial.println("Temperatura -> ");
    Serial.println(String(temperatura).c_str());
    Serial.println("Umidade -> ");
    Serial.println(String(umidade).c_str());
    
    MQTT.publish(topicoTemperatura, String(temperatura).c_str(), true);
    MQTT.publish(topicoUmidade, String(umidade).c_str(), true);

    delay(5000);
}

//função para que o sensor meça os dados
void medirDados() {
  //atribuição do valor medido a sua respectiva variável de umidade
  umidade = dht.readHumidity();
  //atribuição do valor medido a sua respectiva variável de temperatura
  temperatura = dht.readTemperature(false);
  //tempo de espera entre as medições
  delay(2500);
}

//programa principal
void loop() 
{   
    //garante funcionamento das conexões WiFi e ao broker MQTT
    VerificaConexoesWiFIEMQTT();

    //função para que o sensor utilizado meça os dados
    medirDados();
  
    //envia o status de todos os outputs para o Broker no protocolo esperado
    EnviaEstadoOutputMQTT();
 
    //keep-alive da comunicação com broker MQTT
    MQTT.loop();
}
