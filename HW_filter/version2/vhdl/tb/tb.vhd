library ieee;

use std.textio.all;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_textio.all;

use work.multV2_pkg.all;

entity mult_tb is
end entity;

architecture beha of mult_tb is
  component multDaddaRoorda
    generic (N: positive :=8);
    port (
      multiplier:     in std_logic_vector (N-1 downto 0);
      multiplicand:   in std_logic_vector (N-1 downto 0);
      product:        out std_logic_vector (2*(N-1) downto 0)
    );
  end component;

  file file_samples  :text;
  file vhd_results   :text;

  signal r_multiplier   : std_logic_vector(WL-1 downto 0);
  signal r_multiplicand : std_logic_vector(WL-1 downto 0);
  signal w_product      : std_logic_vector(2*(WL-1) downto 0);

begin
  UUT: multDaddaRoorda
    generic map(
    N => WL
    )
    port map(
    multiplier    => r_multiplier,
    multiplicand  => r_multiplicand,
    product       => w_product
    );

  write_result: process
    variable v_inLine       : line;
    variable v_outLine      : line;
    variable v_multiplier   : std_logic_vector(WL-1 downto 0);
    variable v_multiplicand : std_logic_vector(WL-1 downto 0);
    variable v_space        : character;
  begin
    file_open(file_samples, "samples.txt", read_mode);
    file_open(vhd_results,  "hw_result.txt", write_mode);

    while not endfile(file_samples) loop
      readline(file_samples, v_inLine);
      read(v_inLine, v_multiplier);
      read(v_inLine, v_space);
      read(v_inLine, v_multiplicand);

      r_multiplier<=v_multiplier;
      r_multiplicand<=v_multiplicand;

      wait for 50 ns;

      write (v_outLine, w_product, right, 2*(WL-1));
      writeline(vhd_results,v_outLine);
    end loop;
    file_close(file_samples);
    file_close(vhd_results);
    wait;
  end process write_result;
end architecture;
