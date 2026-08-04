package rpg;

import javax.swing.JFrame;

public class Main {
	
	public static void main(String[] args) {

		JFrame window = new JFrame();
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		window.setResizable(false);
		window.setTitle("java-rpg");
		window.setLocationRelativeTo(null); //null defaults to centre
		window.setVisible(true);

		GamePanel gamePanel = new GamePanel();
		window.add(gamePanel);
		window.pack();

		gamePanel.startGameThread();
	}

	
}
