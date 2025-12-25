import { useState } from "react";
import { Helmet } from "react-helmet";
import { Heart, Phone, Clock, Shield } from "lucide-react";
import AdCarousel from "@/components/AdCarousel";
import AppointmentDialog from "@/components/AppointmentDialog";

const Index = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  return (
    <>
      <Helmet>
        <title>Medical Care | Book Your Appointment Today</title>
        <meta
          name="description"
          content="Expert medical care with specialized doctors. Book your appointment online and get personalized healthcare services."
        />
      </Helmet>

      <div className="min-h-screen bg-gradient-soft">
        {/* Header */}
        <header className="w-full py-6 px-4 sm:px-8">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center shadow-glow">
                <Heart className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="font-display font-bold text-xl text-foreground">MediCare</h1>
                <p className="text-sm text-muted-foreground font-body">Your Health Partner</p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <a href="tel:+00123456789" className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors font-body">
                <Phone className="w-4 h-4" />
                00 123 456 789
              </a>
              <button
                onClick={() => setIsDialogOpen(true)}
                className="bg-gradient-primary text-primary-foreground px-6 py-2.5 rounded-full font-display font-semibold shadow-soft hover:shadow-glow transition-all duration-300"
              >
                Book Now
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-4 py-8 sm:py-12">
          {/* Hero Section */}
          <div className="text-center mb-10 animate-fade-up">
            <span className="inline-block px-4 py-1.5 bg-primary-light text-primary rounded-full text-sm font-body font-medium mb-4">
              ✨ Trusted Healthcare Services
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-foreground mb-4">
              Quality Healthcare at Your
              <span className="text-gradient block mt-1">Fingertips</span>
            </h2>
            <p className="text-muted-foreground font-body max-w-2xl mx-auto text-lg">
              Click on our advertisement below to book your appointment and receive
              personalized medical consultation from our expert team.
            </p>
          </div>

          {/* Ad Carousel */}
          <section className="mb-16 animate-slide-up" style={{ animationDelay: "200ms" }}>
            <AdCarousel onAdClick={() => setIsDialogOpen(true)} />
          </section>

          {/* Features */}
          <section className="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-6 animate-fade-up" style={{ animationDelay: "400ms" }}>
            <div className="bg-card rounded-2xl p-6 shadow-card hover:shadow-glow transition-all duration-300 group">
              <div className="w-14 h-14 bg-primary-light rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Clock className="w-7 h-7 text-primary" />
              </div>
              <h3 className="font-display font-bold text-lg text-foreground mb-2">24/7 Support</h3>
              <p className="text-muted-foreground font-body text-sm">
                Our healthcare team is available round the clock for your medical needs.
              </p>
            </div>

            <div className="bg-card rounded-2xl p-6 shadow-card hover:shadow-glow transition-all duration-300 group">
              <div className="w-14 h-14 bg-medical-lavender rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Shield className="w-7 h-7 text-primary" />
              </div>
              <h3 className="font-display font-bold text-lg text-foreground mb-2">Expert Doctors</h3>
              <p className="text-muted-foreground font-body text-sm">
                Consultation with certified specialists in various medical fields.
              </p>
            </div>

            <div className="bg-card rounded-2xl p-6 shadow-card hover:shadow-glow transition-all duration-300 group">
              <div className="w-14 h-14 bg-medical-mint rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Phone className="w-7 h-7 text-primary" />
              </div>
              <h3 className="font-display font-bold text-lg text-foreground mb-2">Quick Response</h3>
              <p className="text-muted-foreground font-body text-sm">
                We'll call you back immediately after booking to confirm your appointment.
              </p>
            </div>
          </section>

          {/* Mobile CTA */}
          <div className="fixed bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-background via-background to-transparent md:hidden">
            <button
              onClick={() => setIsDialogOpen(true)}
              className="w-full bg-gradient-primary text-primary-foreground py-4 rounded-xl font-display font-semibold shadow-glow"
            >
              Book Your Appointment
            </button>
          </div>
        </main>

        {/* Footer */}
        <footer className="py-8 text-center text-muted-foreground font-body text-sm border-t border-border/50">
          <p>© 2025 MediCare. All rights reserved. Your health is our priority.</p>
        </footer>

        {/* Appointment Dialog */}
        <AppointmentDialog
          isOpen={isDialogOpen}
          onClose={() => setIsDialogOpen(false)}
        />
      </div>
    </>
  );
};

export default Index;
