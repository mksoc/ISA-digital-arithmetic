library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity approx_compTB is
end approx_compTB;

architecture behavior of approx_compTB is

    component approx_comp_4to2 is
        port (
          input: in std_logic_vector(3 downto 0);
          output: out std_logic_vector(1 downto 0)
        ) ;
    end component;

    signal input_int: unsigned(3 downto 0);

begin

    input_gen : process
        variable count: natural := 0;
    begin
        input_int <= to_unsigned(count, 4);

        if count = 16 then
            wait;
        else
            count := count + 1;
            wait for 10 ns;
        end if ;
    end process ; -- input_gen


    comp: approx_comp_4to2 port map (input => std_logic_vector(input_int));

end behavior ; -- behavior