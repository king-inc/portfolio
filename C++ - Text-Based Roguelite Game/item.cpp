#include "Item.h"

void GameObject()
{
	GameObject::GameObject(int hp) : m_hp(hp)
	{
		std::cout << "Creating GameObject with " << hp << " health\n"
	}

	void GameObject::damage(int dmg)
	{
		m_hp -= dmg;
		std::cout << "HP. GameObject has " << m_hp << "HP left\n" << "GameObject got damaged: -" << dmg 
	}

Item::~IItem()
{

}
