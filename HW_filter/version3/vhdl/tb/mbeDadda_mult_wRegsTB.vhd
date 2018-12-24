library ieee;
library work;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.multV3_pkg.all;
use STD.textio.all;
use ieee.std_logic_textio.all;

entity mbeDadda_mult_WRegsTB is
	generic(Tclk: time := 20 ns);
end entity;

architecture beh of mbeDadda_mult_WRegsTB is

	-- fast multiplier with radix-4 modified Booth encoding, with Roorda's trick, CSA+fast adder Dadda tree
	component mbeDadda_mult_wRegs is
		port ( 
			clk: std_logic;
			x,											-- multiplicand
			y: in std_logic_vector(WL-1 downto 0);		-- multiplier

			p: out std_logic_vector(WL-1 downto 0) );	-- product
	end component;

	constant iFilePath: string := "../common/multSample.txt";
	constant oFilePath: string := "../common/mult_HW-output.txt";
	constant oBehFilePath: string := "../common/mult_SW-output.txt";

	file fileIn: text;
	file fileOut: text;
	file fileOutBeh: text;

	signal clk: std_logic := '0';

	signal x, y, p: std_logic_vector(WL-1 downto 0);

	signal pBehFullPrecision: std_logic_vector(2*WL-1 downto 0);
	signal pBeh: std_logic_vector(WL-1 downto 0);

begin

	-- clk generation
	clk <= not clk after Tclk/2;

	-- DUT multiplier instantiation
	DUT: mbeDadda_mult_WRegs
		port map (
			clk => clk,
			x => x,
			y => y,
			p => p );

	-- behavioural multiplier instantiation
	pBehFullPrecision <= std_logic_vector(signed(x)*signed(y));
	pBeh <= pBehFullPrecision((WL_INT+2*WL_FRAC)-1 downto (WL-WL_INT));

	-- read input, elaborate, write back output
	readWrite_process: process

	variable inLine: line;
	variable outLine: line;
	variable xIn: std_logic_vector(WL-1 downto 0);
	variable yIn: std_logic_vector(WL-1 downto 0);
	variable separator: character;
	variable isFirstInput: boolean := true;

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

				wait for Tclk;

				if (isFirstInput = true) then
					isFirstInput := false;
				else
					write(outLine, p, right, WL);
					writeline(fileOut, outLine);
				end if;

				write(outLine, pBeh, right, WL);
				writeline(fileOutBeh, outLine);
				
			end loop;

			-- write the last output
			wait for Tclk;
			write(outLine, p, right, WL);
			writeline(fileOut, outLine);

			file_close(fileIn);
			file_close(fileOut);
    		file_close(fileOutBeh);

    		wait;

		end process;

end architecture ; -- arch