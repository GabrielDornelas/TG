#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN 3         // Pino em que será conectado o sensor
#define DHTTYPE DHT11    // Versão do sensor
DHT dht(DHTPIN, DHTTYPE);// Criação objeto DHT
//String sinais; // Variável usada para enviar os sinais
void setup() {
  Serial.begin(9600); //Inicia comunicação serial    
  delay(6000); // Aguarda o sensor armar           
  dht.begin(); // Inicializa o sensor
}

void loop() {
 
  int h = dht.readHumidity();    // Leitura da umidade 
  int t = dht.readTemperature(); // Leitura da Temperatura em Celsius
  // Verificar por erros
  //if (isnan(h) || isnan(t)) {    
  //  return;}
  //Linha que envia os sinais do sensor via Serial para gravar no BD
  //sinais = String(t);
  Serial.println(t);
  delay(1000); //Aguarda 10 segundos
}
