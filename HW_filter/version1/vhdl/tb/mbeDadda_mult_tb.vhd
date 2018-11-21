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

	constant iFilePath: string := "/home/matteo/git/ISA-digital-arithmetic/HW_filter/version1/common/fileIn.txt";
	constant oFilePath: string := "/home/matteo/git/ISA-digital-arithmetic/HW_filter/version1/common/fileOut.txt";
	constant oBehFilePath: string := "/home/matteo/git/ISA-digital-arithmetic/HW_filter/version1/common/fileOutBeh.txt";

	file fileIn: text;
	file fileOut: text;
	file fileOutBeh: text;

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
	pBeh <= pBehFullPrecision((WL_INT+2*WL_FRAC)-1 downto (WL-WL_INT));


	readWrite_process: process

	variable inLine: line;
	variable outLine: line;
	variable xIn: std_logic_vector(WL-1 downto 0);
	variable yIn: std_logic_vector(WL-1 downto 0);
	variable separator: character;

		begin

			file_open(fileIn, iFilePath,  read_mode);
			file_open(fileOut, oFilePath,  write_mode);
			file_open(fileOutBeh, oBehFilePath,  write_mode);

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