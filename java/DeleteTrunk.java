public class DeleteTrunk {
    public static void main(String[] args) throws Exception {
        String trunkSid = System.getenv("TRUNK_SID");
        if (trunkSid == null || trunkSid.isEmpty()) {
            System.err.println("Error: TRUNK_SID environment variable is required");
            System.exit(1);
        }

        System.out.printf("Deleting trunk %s...%n", trunkSid);
        String result = _Client.delete(String.format("/trunks?trunk_sid=%s", trunkSid));
        System.out.println("Trunk deleted successfully!");
    }
} 