import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { format } from "date-fns";
import { Calendar as CalendarIcon, User, Phone, Heart, AlertCircle, Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";

const formSchema = z.object({
  patientName: z.string().min(2, "Name must be at least 2 characters").max(100),
  phoneNumber: z.string().min(10, "Please enter a valid phone number").max(15),
  symptoms: z.string().min(10, "Please describe your symptoms in detail").max(500),
  severity: z.enum(["low", "medium", "high"], {
    required_error: "Please select severity level",
  }),
  appointmentDate: z.date({
    required_error: "Please select an appointment date",
  }),
});

type FormData = z.infer<typeof formSchema>;

interface AppointmentDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

const AppointmentDialog = ({ isOpen, onClose }: AppointmentDialogProps) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      patientName: "",
      phoneNumber: "",
      symptoms: "",
    },
  });

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true);
    
    try {
      // TODO: This will call the edge function to save to CRM and trigger call
      console.log("Submitting appointment:", data);
      
      // Simulate API call for now
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      toast({
        title: "Appointment Booked Successfully! 🎉",
        description: "Our team will call you shortly to confirm your appointment.",
      });
      
      form.reset();
      onClose();
    } catch (error) {
      toast({
        title: "Something went wrong",
        description: "Please try again or call us directly.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "low":
        return "text-medical-teal";
      case "medium":
        return "text-amber-500";
      case "high":
        return "text-medical-coral";
      default:
        return "text-muted-foreground";
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto bg-gradient-card border-primary/20">
        <DialogHeader className="text-center pb-4">
          <div className="mx-auto w-16 h-16 bg-primary-light rounded-full flex items-center justify-center mb-4 animate-fade-up">
            <Heart className="w-8 h-8 text-primary" />
          </div>
          <DialogTitle className="text-2xl font-display text-foreground">
            Book Your Appointment Here!
          </DialogTitle>
          <DialogDescription className="text-muted-foreground font-body">
            Fill in your details and we'll get back to you shortly
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
            {/* Patient Name */}
            <FormField
              control={form.control}
              name="patientName"
              render={({ field }) => (
                <FormItem className="animate-fade-up" style={{ animationDelay: "100ms" }}>
                  <FormLabel className="font-display flex items-center gap-2">
                    <User className="w-4 h-4 text-primary" />
                    Patient Name
                  </FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Enter your full name"
                      className="bg-card border-border/50 focus:border-primary transition-colors"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Phone Number */}
            <FormField
              control={form.control}
              name="phoneNumber"
              render={({ field }) => (
                <FormItem className="animate-fade-up" style={{ animationDelay: "150ms" }}>
                  <FormLabel className="font-display flex items-center gap-2">
                    <Phone className="w-4 h-4 text-primary" />
                    Phone Number
                  </FormLabel>
                  <FormControl>
                    <Input
                      type="tel"
                      placeholder="Enter your phone number"
                      className="bg-card border-border/50 focus:border-primary transition-colors"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Current Health Symptoms */}
            <FormField
              control={form.control}
              name="symptoms"
              render={({ field }) => (
                <FormItem className="animate-fade-up" style={{ animationDelay: "200ms" }}>
                  <FormLabel className="font-display flex items-center gap-2">
                    <Heart className="w-4 h-4 text-primary" />
                    Current Health Symptoms
                  </FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Please describe your current health symptoms..."
                      className="bg-card border-border/50 focus:border-primary transition-colors min-h-[100px] resize-none"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Severity Level */}
            <FormField
              control={form.control}
              name="severity"
              render={({ field }) => (
                <FormItem className="animate-fade-up" style={{ animationDelay: "250ms" }}>
                  <FormLabel className="font-display flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-primary" />
                    Level of Severity
                  </FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger className="bg-card border-border/50 focus:border-primary">
                        <SelectValue placeholder="Select severity level" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="low">
                        <span className="flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-medical-teal" />
                          Low - Mild symptoms
                        </span>
                      </SelectItem>
                      <SelectItem value="medium">
                        <span className="flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-amber-500" />
                          Medium - Moderate concern
                        </span>
                      </SelectItem>
                      <SelectItem value="high">
                        <span className="flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-medical-coral" />
                          High - Urgent attention needed
                        </span>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Appointment Date */}
            <FormField
              control={form.control}
              name="appointmentDate"
              render={({ field }) => (
                <FormItem className="animate-fade-up" style={{ animationDelay: "300ms" }}>
                  <FormLabel className="font-display flex items-center gap-2">
                    <CalendarIcon className="w-4 h-4 text-primary" />
                    Book Your Appointment
                  </FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          className={cn(
                            "w-full justify-start text-left font-normal bg-card border-border/50 hover:border-primary hover:bg-card",
                            !field.value && "text-muted-foreground"
                          )}
                        >
                          <CalendarIcon className="mr-2 h-4 w-4 text-primary" />
                          {field.value ? format(field.value, "PPP") : "Pick a date"}
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={field.value}
                        onSelect={field.onChange}
                        disabled={(date) =>
                          date < new Date() || date < new Date("1900-01-01")
                        }
                        initialFocus
                        className="pointer-events-auto"
                      />
                    </PopoverContent>
                  </Popover>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-gradient-primary hover:opacity-90 text-primary-foreground font-display font-semibold py-6 rounded-xl shadow-glow transition-all duration-300 hover:shadow-soft animate-fade-up"
              style={{ animationDelay: "350ms" }}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Booking...
                </>
              ) : (
                "Submit & Book Appointment"
              )}
            </Button>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
};

export default AppointmentDialog;
