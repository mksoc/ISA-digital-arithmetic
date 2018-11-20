library ieee;
library work;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.multV1_pkg.all;
use STD.textio.all;
use ieee.std_logic_textio.all;

entity mbeDadda_mult_tb is
	generic(multDelay : time := 20 ns);
end entity;

architecture beh of mbeDadda_mult_tb is

	-- fast multiplier with radix-4 modified Booth encoding, with Roorda's trick, CSA+fast adder Dadda tree
	component mbeDadda_mult is
		port ( 
			x,											-- multiplicand
			y: in std_logic_vector(WL-1 downto 0);		-- multiplier

			p: out std_logic_vector(WL-1 downto 0) );	-- product
	end component;

	file fileIn: text;
	file fileOut: text;

	signal x, y, p: std_logic_vector(WL-1 downto 0);

	signal pBehFullPrecision: std_logic_vector(2*WL-1 downto 0);
	signal pBeh: std_logic_vector(WL-1 downto 0);

begin

	DUT: mbeDadda_mult
		port map (
			x => x,
			y => y,
			p => p );

	pBehFullPrecision <= std_logic_vector(signed(x)*signed(y));
	pBeh <= pBehFullPrecision(WL-1 downto 0);


	readWrite_process: process

	variable inLine: line;
	variable outLine: line;
	variable xIn: std_logic_vector(WL-1 downto 0);
	variable yIn: std_logic_vector(WL-1 downto 0);
	variable separator: character;

		begin

			file_open(fileIn, "in.txt",  read_mode);
			file_open(fileOut, "out.txt",  write_mode);
			file_open(fileOutBeh, "outBeh.txt",  write_mode);

			while not endfile(fileIn) loop
				readline(fileIn, inLine);
				read(inLine, xIn);
				read(inLine, separator);
				read(inLine, yIn);

				x <= xIn;
				y <= yIn;

				wait for multDelay;

				write(outLine, p, right, WL);
				writeline(fileOut, outLine);

				write(outLine, pBeh, right, WL);
				writeline(fileOutBeh, outLine);
			end loop;

			file_close(fileIn);
			file_close(fileOut);
    		file_close(fileOutBeh);

    		wait;

		end process;

end architecture ; -- arch