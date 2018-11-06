-- file 'reg.vhd'
-- enable and async reset_n
library ieee;
use ieee.std_logic_1164.all;

entity reg is
    generic (N: positive := 8);
    port (D: in std_logic_vector(N-1 downto 0);
          clock, reset_n, enable: in std_logic;
          Q: out std_logic_vector(N-1 downto 0));
end reg;

architecture behavior of reg is
begin
    process (clock, reset_n)
    begin
		if (reset_n = '0') then
			Q <= (others => '0');
		else
			if (clock'event and clock = '1') then
				if (enable = '1') then
					Q <= D;
				end if;
			end if;
        end if;
    end process;
end behavior;