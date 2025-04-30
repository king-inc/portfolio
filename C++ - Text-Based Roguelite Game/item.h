#pragma once

#include "ItemID.h"

#include <iostream>
#include <string>

namespace temp
{
	class Object
	{
	public:
		Object(int hp);
		virtual void damage(int dmg);
    #define IMPLEMENT_ITEM_NAME(_name) std::string name() override {return #_name;}

    class Item
    {
      public:
	    virtual ~Item();

	    virtual void use(temp::GameObject* target) = 0;
	    virtual ItemID id() = 0;

    private:
    {}

    }
	private:
		int m_hp;
	};

};
