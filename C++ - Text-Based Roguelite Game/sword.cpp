#include "sword.h"


sword::sword(int damage) : m_dmg(damage)
{
}

void sword::use(temp::GameObject* hit)
{
	hit::damage(m_dmg);
}
