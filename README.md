Tämä on Päivölän opiston matematiikkavalmennusviikonloppuna tehty harjoitusprojekti, jonka tavoitteena oli löytää tehokas tapa laskea hirvimäärä metsästysalueella ja verrata eri tapojen virheet ja kustannukset.

Tässä teoreettisesti ostamme skannerin ja dronen, jonka lennättää palkattu lennättäjä. Drone skannaa osan alueesta ja löytää hirviä niiden koon, värin ja liikkeiden perusteella.

Tähän oli tehtävä simulaatio tästä skanneri-dronesta ja hirvistä. Simulaation tarkoitus oli katsoa mahdollisia virhelähteitä ja laskea virheprosentin. Hirvet yleensä liikkuvat ruokaa etsiessä ja muutenkin, joten ensiksi piti löytää tietoa hirvistä. Drone voi skannata saman hirven kahdesti, jos toinen liikkuu, joten oli löydettävä paras tapa lennättää drone.

Simulaatio oli tehty Python-koodilla terminaaliohjelmana. Se voi olla nopea - suuria simulaatiomääriä varten ja voi olla hidas, mutta visualisoinnilla, mikä voi auttaa virhelähteiden etsimistä ja prosessin hahmottamista.

Parametrit olivat generoitu Latinalaisella hyperkuutiolla (Latin hypercube sampling), minkä vuoksi saimme otokset tilastoon mahdollisimman tehokkaasti ja realistisesti.

Esitimme droonin ja skannerin hintoineen hieman humoristisessa slide-esityksessämme.

