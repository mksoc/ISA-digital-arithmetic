library ieee;
use ieee.std_logic_1164.all;

entity iir_filterCU is
    port (
        -- from external world
        clk, rst_n: in std_logic;
        vIn: in std_logic;
        -- controls to DP
        input_regs_en, sw_regs_en, out_reg_en: out std_logic;
        -- to external world
        vOut : out std_logic 
    );
end entity;

architecture behavior of iir_filterCU is
	type stateType is (IDLE, FIRST_SAMPLE, SAMPLE, PAUSE);
	signal presentState, nextState: stateType;

begin
    ps_process: process (clk, rst_n)
        begin
            if (rst_n = '0') then
                presentState <= IDLE;
            else
                if (clk'event and clk = '1') then
                    presentState <= nextState;
                end if;
            end if;
        end process;

    ns_process: process (presentState, vIn)
        begin
            case presentState is
                when IDLE =>
                    if (vIn = '1') then
                        nextState <= FIRST_SAMPLE;
                    else
                        nextState <= IDLE;
                    end if;

                when FIRST_SAMPLE =>
                    if (vIn = '1') then
                        nextState <= SAMPLE;
                    else
                        nextState <= PAUSE;
                    end if;
                    
                when SAMPLE => 
                    if (vIn = '1') then
                        nextState <= SAMPLE;
                    else
                        nextState <= PAUSE;
                    end if;       
                    
                when PAUSE =>
                    if (vIn = '1') then
                        nextState <= FIRST_SAMPLE;
                    else
                        nextState <= IDLE;
                    end if;  

                when others => 
                    nextState <= IDLE;
            end case;
        end process;

    out_process: process(presentState)
        begin
            -- default assignments  
            sw_regs_en <= '0';
            out_reg_en <= '0';
            vOut <= '0';

            case presentState is
                when IDLE =>

                when FIRST_SAMPLE => 
                    sw_regs_en <= '1';
                    out_reg_en <= '1';
                    
                when SAMPLE => 
                    sw_regs_en <= '1';
                    out_reg_en <= '1';
                    vOut <= '1';

                when PAUSE => 
                    vOut <= '1';

            end case;
        end process;

    -- "mealy" signal assignments
    -- vIn directly to input register and coefficient register enable due to timing constraints,
    -- this avoids the need to delay of another clock cycle input data
    input_regs_en <= vIn;

end architecture behavior;