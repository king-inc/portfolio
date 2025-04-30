////for this code and that of the general inventory, and sword I began by following along with this article:https://codereview.stackexchange.com/questions/194561/c-inventory-system but I simply used it as inspiration before designing this for this specific task as some of the features within that code weren't useful to this scenario within our game, also the sword.cpp and sword.h are clones of this file, however with different characteristics so the same reference applies

#include "DamagePotion.h"


DamagePotion::DamagePotion(int damage) : m_dmg(damage)
{
}

void DamagePotion::use(temp::GameObject* hit)
{
	hit::damage(m_dmg);
}
