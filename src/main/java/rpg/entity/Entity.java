package rpg.entity;

public class Entity {

	public enum DIRECTION {UP, RIGHT, DOWN, LEFT}
	
	public int x, y, speed;
	public DIRECTION direction;

	public int spriteCounter = 0;
	public int spriteNum = 1;
}
