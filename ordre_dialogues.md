##### **Finalisation du rendu :**



NOUVEAUX :

* Possibilité de retourner au hub avec l'argent gagné (+10/ennemi, +50 mini-boss, +100 boss)
* Après victoire au casino (suite du mini-boss) : dialogue(display, "postnutclarity.txt", "player.txt")
* Défaite boss (exfemme) : dialogue(display, "defaite\_boss.txt", "player.txt")
* Défaite ennemi basique : dialogue(display, "dead.txt", "player.txt")
* ennemi basique : 10 hp // 10 sh // 5 st
* EMPLACEMENTS : (01)  - 1 ennemi, (10) - 2 ennemis, (30) - 1 ennemi + "page1.txt", (31) - 1 ennemi, (22) - 1 ennemi, (34) - 2 ennemis,

(60) - 2 ennemis, (50) - "page2.txt", (72) - "page3.txt", (81) - 1 ennemi, (80) - 1 ennemi, (23) - 1 ennemi, (15) - 2 ennemis, (14) - "page4.txt", (45) 1 ennemi, (64) - 3 ennemis,

(95) - 2 ennemis, (84) - "page5.txt"

* dialogue retour au hub : script "comeback.py", fonction : retour(display) -> return True/False
* Emplacement du mini-boss après l'avoir vaincu : dialogue(display, "alternative.txt", "player.txt")
* Pour les pages, commande : dialogue(display, "page1.txt", "book.txt")



Démarrage casino "unfair" -> Fait !

\[casino\_game(display, starting\_money=20, mode="unfair")]

\[dialogue(display, "dette\_casino.txt", "arlequin.txt")]



Hub : casino "balanced", banque, magasin, maison -> Fait !

Ajouter dialogue "maison.txt" devant la maison "A vendre ! Deux chambres, non meublé. Contacter le... (\*C'est, ou plutôt, c'était ma maison. Ce n'est plus chez moi désormais.\*)"

\[dialogue(display, "maison.txt", "house.txt")]



Ennemi intermédiaire/mini-boss : 20 hp // 15 sh // 10 st

\[combat(display, player, enemy, bag, "arlequin.txt")]



Ajouter dialogue "bonheur1.txt" à la fin du combat "(\*J'ai réussi ! J'avais oublié cette sensation de victoire, le sentiment d'avoir de la valeur. Pourtant, là-bas aussi c'était pareil à l'époque : j'étais tout-puissant, intouchable. J'aimerais regoûter au plaisir du gain, mais...\*)"

\[dialogue(d, "bonheur1.txt", "player.txt")]



\+ flashback = casino "fair"

\[casino\_game(display, starting\_money=100, mode="fair")]



Possibilité de retourner au hub avec l'argent gagné (+10/ennemi, +50 mini-boss)



Dialogue "exfemme.txt" : "Quel allure pathétique, tu n'as pas changé. Toujours en quête de quelques pièces à gaspiller au casino ?

Ce n'est pas la peine d'essayer de me convaincre, je ne reviendrai pas. Ils avaient raison, notre divorce était invitable. J'espère que tu as conscience d'avoir

TOUT GACHE, TOUT GACHE, TOUT GACHE !!!"

\[dialogue(display, "exfemme.txt", "femme.txt")]



Ennemi final/boss : 40 hp // 20 sh // 15 st

\[combat(display, player, enemy, bag, enemy\_sprite="femme.txt")]

\+ (optionnel) flashback = casino "unfair"

\[casino\_game(display, starting\_money=100, mode="unfair")]



Ajouter dialogue "redemption1.txt" à la fin du combat "(\*Cela aussi, je l'avais oublié. J'ai enfoui ces souvenirs douloureux dans ma mémoire, j'ai fui dans le jeu.

Elle m'en veut, c'est normal. Pourtant, j'aurais pu tant lui offrir si j'avais été riche ! Etait-ce important pour être heureux, ou suffisait-il d'être ensemble ?\*)"

\[dialogue(display, "redemption1.txt", "player.txt")]



Possibilité de retourner au hub avec l'argent gagné (+10/ennemi, +50 mini-boss, +100 boss)

